import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { throwError, catchError, Observable, tap } from 'rxjs';
import { environment } from '../../environments/environment';
import { Router } from '@angular/router';
import { jwtDecode } from 'jwt-decode';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiLoginEndpoint = environment.backendUrl + '/login';
  private apiLogoutEndpoint = environment.backendUrl + '/logout';

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

  getRefreshToken(): string | null {
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
}