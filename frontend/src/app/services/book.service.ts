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
  private apiGenresEndpoint = environment.backendUrl + '/genres';
  private apiBooksGenresEndpoint = environment.backendUrl + '/books-genres';
  private apiAssociateBookToGenreEndpoint = this.apiBooksGenresEndpoint + '/associate-book-to-genre';
  private apiGenresByBookEndpoint = this.apiBooksGenresEndpoint + '/genres-by-book';

  constructor(private http: HttpClient, private authService: AuthService) { }

  getSortedBooks(col: string, order: string): Observable<any> {
    return this.authService.addHttpHeaders().pipe(
      switchMap((headers) => {
        return this.http.get<any>(`${ this.apiBooksEndpoint }?col=${ col }&order=${ order }`, { headers }).pipe(
          catchError((error) => {
            return throwError(() => error.error.message || 'Could not fetch book books');
          })
        );
      })
    );
  }

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
    );
  }

  getGenres(): Observable<any> {
    return this.authService.addHttpHeaders().pipe(
      switchMap((headers) => {
        return this.http.get<any>(this.apiGenresEndpoint, { headers }).pipe(
          catchError((error) => {
            return throwError(() => error.error.message || 'Could not fetch genres');
          })
        );
      })
    );
  }

  getSortedGenres(col: string, order: string) {
    return this.authService.addHttpHeaders().pipe(
      switchMap((headers) => {
        return this.http.get<any>(`${this.apiGenresEndpoint}?col=${ col }&order=${ order }`, { headers }).pipe(
          catchError((error) => {
            return throwError(() => error.error.message || 'Could not fetch genres');
          })
        );
      })
    );
  }

  getAssociatedGenres(bookId: string) {
    return this.authService.addHttpHeaders().pipe(
      switchMap((headers) => {
        return this.http.get<any>(`${this.apiGenresByBookEndpoint}/${bookId}`, { headers }).pipe(
          catchError((error) => {
            return throwError(() => error.error.message || 'Could not fetch genres for book');
          })
        );
      })
    );
  }

  associateBookToGenre(bookId: string, genreId: number) {
    const body = {
      'bookId': bookId,
      'genreId': genreId
    };
    return this.authService.addHttpHeaders().pipe(
      switchMap((headers) => {
        return this.http.post<any>(this.apiAssociateBookToGenreEndpoint, body, { headers }).pipe(
          catchError((error) => {
            return throwError(() => error.error.message || 'Could not associate book to genre');
          })
        );
      })
    );
  }

  unassociateBookToGenre(bookId: string, genreId: number) {
    return this.authService.addHttpHeaders().pipe(
      switchMap((headers) => {
        return this.http.delete<any>(`${this.apiBooksGenresEndpoint}/${bookId}/${genreId}`, { headers }).pipe(
          catchError((error) => {
            return throwError(() => error.error.message || 'Could not unassociate book to genre');
          })
        );
      })
    );
  }

  addGenre(genreName: string): Observable<any> {
    const body = {
      'genre': genreName
    };
    return this.authService.addHttpHeaders().pipe(
      switchMap((headers) => {
        return this.http.post<any>(this.apiGenresEndpoint, body, { headers }).pipe(
          catchError((error) => {
            return throwError(() => error.error.message || 'Could not create genre');
          })
        );
      })
    );
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
    );
  }

  addBook(newBookDetails: any): Observable<any> {
    return this.authService.addHttpHeaders().pipe(
      switchMap((headers) => {
        return this.http.post<any>(this.apiBooksEndpoint, newBookDetails, { headers }).pipe(
          catchError((error) => {
            return throwError(() => error.error.message || 'Could not create book');
          })
        );
      })
    );
  }
}