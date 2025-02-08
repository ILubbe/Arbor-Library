import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { throwError, catchError, Observable, tap, switchMap, of } from 'rxjs';
import { environment } from '../../environments/environment';
import { Router } from '@angular/router';
import { jwtDecode } from 'jwt-decode';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiLoginEndpoint = environment.backendUrl + '/login';
  private apiLogoutEndpoint = environment.backendUrl + '/logout';
  private apiRefreshEndpoint = environment.backendUrl + '/refresh';

  constructor(private http: HttpClient, private router: Router) {}

  login(email: string, password: string): Observable<any> {
    const body = { email, password };
    return this.http.post<any>(this.apiLoginEndpoint, body).pipe(
      catchError((error) => {
        return throwError(() => error.error.message || 'Login failed, please try again');
      })
    );
  }

  getAccessToken(): string | null {
    return localStorage.getItem('accessToken');
  }

  getRefreshToken(): string | null{
    return localStorage.getItem('refreshToken');
  }

  logout(): boolean {
    const refreshToken = this.getRefreshToken();
  
    if (!refreshToken) {
      // If no refresh token is found, logout can't be completed
      return false;
    }
  
    const headers = {
      'Authorization': `Bearer ${refreshToken}`,
      'Content-Type': 'application/json'
    }
    
    this.http.post<any>(this.apiLogoutEndpoint, {}, { headers }).pipe(
      catchError(() => {
        return new Observable<boolean>((observer) => {
          observer.next(false);
          observer.complete();
        });
      }),
      tap(() => {
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
        alert('You have been logged out.');
        this.router.navigateByUrl('/login');
      })
    ).subscribe();
    return true;
  }
  

  getUserRole(): string | null {
    const accessToken = localStorage.getItem('accessToken');
    if (accessToken) {
      try {
        const decodedToken: any = jwtDecode(accessToken);
        return decodedToken.role || null;
      } catch (error) {
        console.error('Error decoding token', error);
        return null;
      }
    }
    return null;
  }

  addHttpHeaders(): Observable<{ [key: string]: string }> {
    const accessToken = this.getAccessToken();
    const refreshToken = this.getRefreshToken();

    if (!accessToken || !refreshToken) {
      this.logout();
      return of({});
    }

    try {
      const decodedAccessToken: any = jwtDecode(accessToken);
      const expirationTime = decodedAccessToken.exp * 1000;

      if (expirationTime < Date.now()) {
        return this.refreshAccessToken(refreshToken).pipe(
          switchMap((response: any) => {
            localStorage.setItem('accessToken', response.accessToken);
            localStorage.setItem('refreshToken', response.refreshToken);

            const headers = {
              'Authorization': `Bearer ${response.accessToken}`,
              'Content-Type': 'application/json'
            };
            return of(headers);
          }),
          catchError((error) => {
            console.error('Token refresh failed', error);
            this.logout();
            return of({}); // return empty headers if refresh fails
          })
        );
      } else {
        const headers = {
          'Authorization': `Bearer ${accessToken}`,
          'Content-Type': 'application/json'
        };
        return of(headers);
      }
    } catch (error) {
      console.error('Invalid access token', error);
      this.logout();
      return of({});
    }
  }

  private refreshAccessToken(refreshToken: string): Observable<any> {
    const headers = {
      'Authorization': `Bearer ${refreshToken}`,
      'Content-Type': 'application/json'
    };

    return this.http.post<any>(this.apiRefreshEndpoint, {}, { headers }).pipe(
      catchError((error) => {
        console.error('Failed to refresh access token', error);
        return of(null);
      })
    );
  }
}