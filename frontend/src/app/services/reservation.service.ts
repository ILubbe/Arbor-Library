import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { throwError, catchError, Observable, switchMap } from 'rxjs';
import { environment } from '../../environments/environment';
import { AuthService } from './auth.service';

@Injectable({
  providedIn: 'root'
})
export class ReservationService {
  private apiReservationsEndpoint = environment.backendUrl + '/reservations';
  private apiMyReservationsEndpoint = this.apiReservationsEndpoint + '/my';

  constructor(private http: HttpClient, private authService: AuthService) { }

  getAllSorted(col: string, order: string, page: number, perPage: number): Observable<any> {
    return this.authService.addHttpHeaders().pipe(
      switchMap((headers) => {
        const url = `${this.apiReservationsEndpoint}?col=${col}&order=${order}&page=${page}&per-page=${perPage}`;
        return this.http.get<any>(url, { headers }).pipe(
          catchError((error) => {
            return throwError(() => error.error.message || 'Could not fetch users');
          })
        );
      })
    );
  }

  getMyReservations(): Observable<any> {
    return this.authService.addHttpHeaders().pipe(
      switchMap((headers) => {
        return this.http.get<any>(this.apiMyReservationsEndpoint, { headers }).pipe(
          catchError((error) => {
            return throwError(() => error.error.message || 'Could not fetch user reservations');
          })
        );
      })
    );
  }

  createMyReservation(bookId: string): Observable<any> {
    const reservationData = {
      bookId: bookId
    };
    return this.authService.addHttpHeaders().pipe(
      switchMap((headers) => {
        return this.http.post(this.apiMyReservationsEndpoint, reservationData, { headers }).pipe(
          catchError((error) => {
            return throwError(() => error.error.message || 'Failed to create reservation');
          })
        );
      })
    );
  }

  cancelMyReservation(reservationId: string): Observable<any> {
    return this.authService.addHttpHeaders().pipe(
      switchMap((headers) => {
        return this.http.delete(`${this.apiMyReservationsEndpoint}/${reservationId}`, { headers }).pipe(
          catchError((error) => {
            return throwError(() => error.error.message || 'Failed to cancel reservation');
          })
        );
      })
    );
  }

  cancelReservation(reservationId: string): Observable<any> {
    return this.authService.addHttpHeaders().pipe(
      switchMap((headers) => {
        return this.http.delete(`${this.apiReservationsEndpoint}/${reservationId}`, { headers }).pipe(
          catchError((error) => {
            return throwError(() => error.error.message || 'Failed to cancel reservation');
          })
        );
      })
    );
  }
}