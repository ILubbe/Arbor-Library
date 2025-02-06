import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { throwError, catchError, Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { AuthService } from './auth.service';

@Injectable({
  providedIn: 'root'
})
export class BookService {
  private apiBooksEndpoint = environment.backendUrl + '/books';

  constructor(private http: HttpClient, private authService: AuthService) { }

  getBookById(id: string): Observable<any> {
    const accessToken = this.authService.getAccessToken();
    const headers = {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json'
    }
    return this.http.get<any>(this.apiBooksEndpoint + '/' + id, { headers }).pipe(
      catchError((error) => {
        return throwError(() => error.error.message || 'Could not book details');
      })
    );
  }
}