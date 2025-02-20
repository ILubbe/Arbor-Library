import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { throwError, catchError, Observable, switchMap } from 'rxjs';
import { environment } from '../../environments/environment';
import { AuthService } from './auth.service';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private apiUserEndpoint = environment.backendUrl + '/users';
  private apiUserProfileEndpoint = environment.backendUrl + '/users/profile';

  constructor(private http: HttpClient, private authService: AuthService) { }

  getSortedUsers(col: string, order: string): Observable<any> {
    return this.authService.addHttpHeaders().pipe(
      switchMap((headers) => {
        return this.http.get<any>(`${this.apiUserEndpoint}?col=${ col }&order=${ order }`, { headers }).pipe(
          catchError((error) => {
            return throwError(() => error.error.message || 'Could not fetch users');
          })
        );
      })
    );
  }

  getUserById(userId: string): Observable<any> {
    return this.authService.addHttpHeaders().pipe(
      switchMap((headers) => {
        return this.http.get<any>(`${this.apiUserEndpoint}/${ userId }`, { headers }).pipe(
          catchError((error) => {
            return throwError(() => error.error.message || 'Could not fetch user details');
          })
        );
      })
    );
  }

  SwitchUserRoleById(userId: string): Observable<any> {
    return this.authService.addHttpHeaders().pipe(
      switchMap((headers) => {
        return this.http.patch<any>(`${this.apiUserEndpoint}/${ userId }`, {}, { headers }).pipe(
          catchError((error) => {
            return throwError(() => error.error.message || 'Could not fetch user details');
          })
        );
      })
    );
  }

  deleteUserById(userId: string): Observable<any> {
    return this.authService.addHttpHeaders().pipe(
      switchMap((headers) => {
        return this.http.delete<any>(`${this.apiUserEndpoint}/${ userId }`, { headers }).pipe(
          catchError((error) => {
            return throwError(() => error.error.message || 'Could not fetch user details');
          })
        );
      })
    );
  }

  getMyProfile(): Observable<any> {
    return this.authService.addHttpHeaders().pipe(
      switchMap((headers) => {
        return this.http.get<any>(this.apiUserProfileEndpoint, { headers }).pipe(
          catchError((error) => {
            return throwError(() => error.error.message || 'Could not fetch user profile');
          })
        );
      })
    );
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
    );
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
    );
  }
}