import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { throwError, catchError, Observable, switchMap } from 'rxjs';
import { environment } from '../../environments/environment';
import { AuthService } from './auth.service';

@Injectable({
  providedIn: 'root'
})
export class BookService {
  private apiBooksEndpoint = environment.backendUrl + '/books';

  constructor(private http: HttpClient, private authService: AuthService) { }

  getBookById(bookId: string): Observable<any> {
    return this.authService.addHttpHeaders().pipe(
      switchMap((headers) => {
        return this.http.get<any>(`${ this.apiBooksEndpoint }/${ bookId }`, { headers }).pipe(
          catchError((error) => {
            return throwError(() => error.error.message || 'Could not fetch book details');
          })
        );
      })
    );
  }

  deleteBookById(bookId: string): Observable<any> {
    return this.authService.addHttpHeaders().pipe(
      switchMap((headers) => {
        return this.http.delete<any>(`${ this.apiBooksEndpoint }/${ bookId }`, { headers }).pipe(
          catchError ((error) => {
            return throwError(() => error.error.message || 'Could not delete book');
          })
        );
      })
    )
  }

  updateBook(bookId: string, updatedBookDetails: any): Observable<any> {
    return this.authService.addHttpHeaders().pipe(
      switchMap((headers) => {
        return this.http.put<any>(`${ this.apiBooksEndpoint }/${ bookId }`, updatedBookDetails, { headers }).pipe(
          catchError((error) => {
            return throwError(() => error.error.message || 'Could not update book');
          })
        );
      })
    )
  }
}