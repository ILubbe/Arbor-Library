import { Component, Input, Output, EventEmitter } from '@angular/core';
import { AuthService } from '../../services/auth.service';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../environments/environment';
import { debounceTime, switchMap } from 'rxjs/operators';
import { Subject } from 'rxjs';
import { FormsModule } from '@angular/forms';

interface SearchResult {
  total: number;
  page: number;
  per_page: number;
  results: any[];
}

@Component({
  selector: 'app-search-bar',
  imports: [FormsModule],
  templateUrl: './search-bar.component.html',
  styleUrl: './search-bar.component.scss'
})
export class SearchBarComponent {
  @Input() fieldOptions: string[] = [];
  @Input() selectedModel: string = 'Book'; // Default to 'Book'
  @Input() selectedField: string = '';
  @Input() perPage: number = 25
  @Output() searchQuery = new EventEmitter<any>();

  query: string = '';
  page: number = 1;
  results: any[] = [];
  total: number = 0;

  lockedQuery: string = '';
  lockedField: string = '';

  private searchSubject = new Subject<string>;

  constructor(private http: HttpClient, private authService: AuthService) {
    this.searchSubject.pipe(
      debounceTime(500),  // wait for 500ms after the user stops typing
      switchMap((query: string) => this.search(query))  // call searchBooks when the user stops typing
    ).subscribe((response: SearchResult) => {
      this.results = response.results;
      this.total = response.total;

      this.page = response.page;
      this.perPage = response.per_page;
    });
  }

  search(query: string) {
    let apiSearchEndpoint = environment.backendUrl + `/search?model=${this.selectedModel}&query=${this.query}&page=${this.page}&limit=${this.perPage}`;
    if (this.selectedField) {
      apiSearchEndpoint += `&field=${this.selectedField}`;
    }

    const accessToken = this.authService.getAccessToken();
    const headers = {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json'
    }

    return this.http.get<SearchResult>(apiSearchEndpoint, { headers });
  }

  onQueryChange(query: string) {
    if (this.query !== this.lockedQuery) {
      this.page = 1;
      this.lockedQuery = this.query; // lock the query
    }
    this.searchSubject.next(query);
    this.searchQuery.emit({
      model: this.selectedModel,
      field: this.selectedField,
      page: this.page,
      limit: this.perPage
    });
  }

  onFieldChange(field: string) {
    this.selectedField = field;
    if (this.selectedField !== this.lockedField) {
      this.page = 1;
      this.lockedField = this.selectedField; // lock the field
    }

    this.onQueryChange(this.query);
  }

  changePage(page: number) {
    this.page = page;
    this.onQueryChange(this.query);
    window.scrollTo(0, 0)
  }

  get totalPages(): number {
    return Math.ceil(this.total / this.perPage);
  }
}
