import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { throwError, catchError, Observable } from 'rxjs';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private apiEndpoint = environment.backendUrl + '/users/profile';

  constructor(private http: HttpClient) { }

  getUserProfile(): Observable<any> {
    const accessToken = localStorage.getItem('accessToken');
    const headers = {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json'
    }
    return this.http.get<any>(this.apiEndpoint, { headers }).pipe(
      catchError((error) => {
        return throwError(() => error.error.message || 'Could not fetch user profile');
      })
    );
  }
}