import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { throwError, catchError, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = 'http://localhost:5000/login'; // TODO variablize this later

  constructor(private http: HttpClient) {}

  login(email: string, password: string): Observable<any> {
    const body = { email, password };
    return this.http.post<any>(this.apiUrl, body).pipe(
      catchError((error) => {
        return throwError(() => error.error.message || 'Login failed, please try again');
      })
    );
  }

  refreshToken(refreshToken: string): Observable<any> {
    const refreshUrl = 'http://localhost:5000/refresh'; // TODO variablize this later
    return this.http.post<any>(refreshUrl, { refreshToken: refreshToken });
  }

  getAccessToken(): string | null {
    return localStorage.getItem('accessToken');
  }


  getRefreshToken(): string | null {
    return localStorage.getItem('refreshToken');
  }

  // Utility method to clear tokens (e.g., on logout)
  clearTokens(): void {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
  }
}