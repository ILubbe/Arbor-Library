import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { throwError, catchError, Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { Router } from '@angular/router';
import { jwtDecode } from 'jwt-decode';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiEndpoint = environment.backendUrl + '/login';

  constructor(private http: HttpClient, private router: Router) {}

  login(email: string, password: string): Observable<any> {
    const body = { email, password };
    return this.http.post<any>(this.apiEndpoint, body).pipe(
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
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    alert('You have been logged out.')
    this.router.navigateByUrl('/login');
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