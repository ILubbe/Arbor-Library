import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { throwError, catchError, Observable } from 'rxjs';
import { environment } from '../../environments/enironment';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiEndpoint = environment.backendUrl + '/login';

  constructor(private http: HttpClient) {}

  login(email: string, password: string): Observable<any> {
    const body = { email, password };
    return this.http.post<any>(this.apiEndpoint, body).pipe(
      catchError((error) => {
        return throwError(() => error.error.message || 'Login failed, please try again');
      })
    );
  }

  refreshToken(refreshToken: string): Observable<any> {
    const apiEndpoint = environment.backendUrl + '/refresh';
    return this.http.post<any>(apiEndpoint, { refreshToken: refreshToken });
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