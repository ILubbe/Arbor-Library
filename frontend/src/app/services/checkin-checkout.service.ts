import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { throwError, catchError, Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { AuthService } from './auth.service';

@Injectable({
  providedIn: 'root'
})
export class CheckinCheckoutService {
  private apiCheckoutEndpoint = environment.backendUrl + '/checkouts';

  constructor(private http: HttpClient, private authService: AuthService) { }

  checkout(userId: string, bookId: string): Observable<any> {
    const accessToken = this.authService.getAccessToken();
    const headers = {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json'
    }
    const checkoutBody = {
      'userId': userId,
      'bookId': bookId
    }
    return this.http.post<any>(this.apiCheckoutEndpoint, checkoutBody, { headers }).pipe(
      catchError((error) => {
        return throwError(() => error.error.message || 'Could not check out book');
      })
    );
  }

  checkin(checkoutId: string): Observable<any> {
    const accessToken = this.authService.getAccessToken();
    const headers = {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json'
    }
    return this.http.patch<any>(`${this.apiCheckoutEndpoint}/${ checkoutId }`, {}, { headers }).pipe(
      catchError((error) => {
        return throwError(() => error.error.message || 'Could not check in book');
      })
    );
  }
}