import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { throwError, catchError, Observable, switchMap } from 'rxjs';
import { environment } from '../../environments/environment';
import { AuthService } from './auth.service';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private apiUserProfileEndpoint = environment.backendUrl + '/users/profile';

  constructor(private http: HttpClient, private authService: AuthService) { }

  getMyProfile(): Observable<any> {
    return this.authService.addHttpHeaders().pipe(
      switchMap((headers) => {
        return this.http.get<any>(this.apiUserProfileEndpoint, { headers }).pipe(
          catchError((error) => {
            return throwError(() => error.error.message || 'Could not fetch user profile');
          })
        );
      })
    )
  }

  updateMyProfile(updatedUserDetails: any): Observable<any> {
    return this.authService.addHttpHeaders().pipe(
      switchMap((headers) => {
        return this.http.put<any>(this.apiUserProfileEndpoint, updatedUserDetails, { headers }).pipe(
          catchError((error) => {
            return throwError(() => error.error.message);
          })
        );
      })
    )
  }

  deleteMyProfile(): Observable<any> {
    return this.authService.addHttpHeaders().pipe(
      switchMap((headers) => {
        return this.http.delete<any>(this.apiUserProfileEndpoint, { headers }).pipe(
          catchError((error) => {
            return throwError(() => error.error.message || 'Could not delete user profile');
          })
        );
      })
    )
  }
}