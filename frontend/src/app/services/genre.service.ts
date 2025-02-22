import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { throwError, catchError, Observable, switchMap } from 'rxjs';
import { environment } from '../../environments/environment';
import { AuthService } from './auth.service';

@Injectable({
  providedIn: 'root'
})
export class GenreService {
  private apiGenresEndpoint = environment.backendUrl + '/genres';

  constructor(private http: HttpClient, private authService: AuthService) { }
  
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

  getAllSorted(col: string, order: string, page: number, perPage: number): Observable<any> {
    return this.authService.addHttpHeaders().pipe(
      switchMap((headers) => {
        const url = `${this.apiGenresEndpoint}?col=${col}&order=${order}&page=${page}&per-page=${perPage}`;
        return this.http.get<any>(url, { headers }).pipe(
          catchError((error) => {
            return throwError(() => error.error.message || 'Could not fetch genres');
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
  
}
