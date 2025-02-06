import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { throwError, catchError, Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { AuthService } from './auth.service';

@Injectable({
  providedIn: 'root'
})
export class ReservationService {
  private apiMyReservationsEndpoint = environment.backendUrl + '/reservations/my';

  constructor(private http: HttpClient, private authService: AuthService) { }

  getMyReservations(): Observable<any> {
    const accessToken = this.authService.getAccessToken();
    const headers = {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json'
    }
    return this.http.get<any>(this.apiMyReservationsEndpoint, { headers }).pipe(
      catchError((error) => {
        return throwError(() => error.error.message || 'Could not fetch user reservations');
      })
    );
  }

  createMyReservation(bookId: string): Observable<any> {
    const accessToken = this.authService.getAccessToken();
    const headers = {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json'
    };
    const reservationData = {
      bookId: bookId
    };
    return this.http.post(this.apiMyReservationsEndpoint, reservationData, { headers }).pipe(
      catchError((error) => {
        return throwError(() => error.error.message || 'Failed to create reservation');
      })
    );
  }

  cancelMyReservation(reservationId: string): Observable<any> {
    const accessToken = this.authService.getAccessToken();
    const headers = {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json'
    };
    return this.http.delete(`${this.apiMyReservationsEndpoint}/${reservationId}`, { headers }).pipe(
      catchError((error) => {
        return throwError(() => error.error.message || 'Failed to cancel reservation');
      })
    );
  }
}