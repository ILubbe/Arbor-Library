import { Observable } from 'rxjs';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { UserService } from '../../../services/user.service';
import { BookService } from '../../../services/book.service';
import { GenreService } from '../../../services/genre.service';
import { CheckinCheckoutService } from '../../../services/checkin-checkout.service';
import { ReservationService } from '../../../services/reservation.service';

export interface ReportService {
  getAllSorted(col: string, order: string, page: number, perPage: number): Observable<any>;
}

@Component({
  selector: 'app-reports',
  imports: [FormsModule],
  templateUrl: './reports.component.html',
  styleUrl: './reports.component.scss'
})

export class ReportsComponent {

  modelOptions: string[] = ['Users', 'Books', 'Genres', 'Checkouts', 'Reservations']
  selectedModel: string = '';
  previousSelectedModel: string = '';
  response: any[] = [];
  total: number = 0;
  tableHeaders: string[] = [];
  col: string = 'id';
  order: string = 'asc';
  page: number = 1;
  perPageOptions: number[] = [10, 25, 50, 100, 250, 500, 1000]
  selectedPerPage: number = 25;
  totalPages: number = 1;
  reportStamp: string = '';
  service!: ReportService;

  constructor(
    private userService: UserService,
    private bookService: BookService,
    private genreService: GenreService,
    private ciCoService: CheckinCheckoutService,
    private reservationService: ReservationService
    ) {}
  
  generateReport(selectedColumn?: string) {
    // report time stamp
    this.reportStamp = new Date().toUTCString();
    if (this.selectedModel) {
      // ensure order is always 'asc' and col is always 'id' when changing models
      if (this.selectedModel !== this.previousSelectedModel) {
        this.order = 'asc';
        this.col = 'id';
      }
      this.previousSelectedModel = this.selectedModel;

      // get correct service
      if (this.selectedModel === 'Users') {
        this.service = this.userService;
      } else if (this.selectedModel === 'Books') {
        this.service = this.bookService;
      } else if (this.selectedModel === 'Genres') {
        this.service = this.genreService;
      } else if (this.selectedModel === 'Checkouts') {
        this.service = this.ciCoService;
      } else if (this.selectedModel === 'Reservations') {
        this.service = this.reservationService;
      }

      const responseItem = this.selectedModel.toLowerCase();

      if (selectedColumn && this.camelCaseToDashCase(selectedColumn) !== this.col) {
        this.col = this.camelCaseToDashCase(selectedColumn);
      }
      this.service.getAllSorted(this.col, this.order, this.page, this.selectedPerPage).subscribe({
        next: (response) => {
          this.response = response[responseItem];
          this.total = response.total;
          this.totalPages = Math.ceil(this.total / this.selectedPerPage);
          this.tableHeaders = this.response.length ? Object.keys(this.response[0]) : [];
          this.reorderHeaders();
        },
        error: (error) => {
          console.error(error || 'Could not fetch report')
        }
      });
    }
  }

  sort(selectedColumn: string) {
    this.page = 1;
    this.order = this.order === 'asc' ? 'desc' : 'asc'; // toggle order
    this.generateReport(selectedColumn);
  }

  changePage(page: number) {
    this.page = page;
    this.generateReport();
  }

  reorderHeaders() {
    const desiredHeaderOrder: { [model: string]: string[] } = {
      'users': ['id', 'email', 'firstname', 'lastname', 'role'],
      'books': ['id', 'title', 'author', 'firstyearpublished', 'bookcondition', 'genres'],
      'genres': ['id', 'genre'],
      'checkouts': ['id', 'userid', 'bookid', 'checkedoutat', 'dueat', 'returned'],
      'reservations': ['id', 'userid', 'bookid', 'reservedat', 'expiresat', 'status']
    };

    const modelKey = this.selectedModel.toLowerCase();
    if (desiredHeaderOrder[modelKey]) {
      // normalize the current headers to lowercase for comparison
      const lowerHeaders = this.tableHeaders.map(header => header.toLowerCase());
      const desiredOrder = desiredHeaderOrder[modelKey];
      let newOrder: string[] = [];

      // reorder headers
      desiredOrder.forEach(desiredKey => {
        const index = lowerHeaders.indexOf(desiredKey);
        if (index !== -1) {
          newOrder.push(this.tableHeaders[index]);
        }
      });

      this.tableHeaders = newOrder;
    }
  }

  // for display
  camelCaseToTitleCase(camelCaseString: string): string {
    return camelCaseString.replace(/([a-z])([A-Z])/g, '$1 $2').replace(/^./, (str) => str.toUpperCase());
  }

  // for urls
  camelCaseToDashCase(camelCaseString: string): string {
    return camelCaseString.replace(/([a-z])([A-Z])/g, '$1-$2').toLowerCase();
  }
}
