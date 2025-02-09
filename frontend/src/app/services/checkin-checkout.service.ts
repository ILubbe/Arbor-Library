import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { throwError, catchError, Observable, switchMap } from 'rxjs';
import { environment } from '../../environments/environment';
import { AuthService } from './auth.service';

@Injectable({
  providedIn: 'root'
})
export class CheckinCheckoutService {
  private apiCheckoutEndpoint = environment.backendUrl + '/checkouts';
  private apiMyCheckoutEndpoint = environment.backendUrl + '/checkouts/my';

  constructor(private http: HttpClient, private authService: AuthService) { }

  checkout(userId: string, bookId: string): Observable<any> {
    const checkoutBody = {
      'userId': userId,
      'bookId': bookId
    }
    return this.authService.addHttpHeaders().pipe(
      switchMap((headers) => {
        return this.http.post<any>(this.apiCheckoutEndpoint, checkoutBody, { headers }).pipe(
          catchError((error) => {
            return throwError(() => error.error.message || 'Could not check out book');
          })
        );
      })
    );
  }

  checkin(checkoutId: string): Observable<any> {
    return this.authService.addHttpHeaders().pipe(
      switchMap((headers) => {
        return this.http.patch<any>(`${this.apiCheckoutEndpoint}/${ checkoutId }`, {}, { headers }).pipe(
          catchError((error) => {
            return throwError(() => error.error.message || 'Could not check in book');
          })
        );
      })
    );
  }

  getMyCheckouts(): Observable<any> {
    return this.authService.addHttpHeaders().pipe(
      switchMap((headers) => {
        return this.http.get<any>(this.apiMyCheckoutEndpoint, { headers }).pipe(
          catchError((error) => {
            return throwError(() => error.error.message || 'Could not fetch user checkouts');
          })
        );
      })
    )
  }
}