import { Observable } from 'rxjs';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { UserService } from '../../../services/user.service';
import { BookService } from '../../../services/book.service';
import { GenreService } from '../../../services/genre.service';
import { CheckinCheckoutService } from '../../../services/checkin-checkout.service';
import { ReservationService } from '../../../services/reservation.service';

export interface ReportService {
  getAllSorted(col?: string, order?: string): Observable<any>;
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
  response: any[] = [];
  tableHeaders: string[] = [];
  order: string = 'desc';
  service!: ReportService;

  constructor(
    private userService: UserService,
    private bookService: BookService,
    private genreService: GenreService,
    private ciCoService: CheckinCheckoutService,
    private reservationService: ReservationService
    ) {}
  
  generateReport(col?: string) {
    if (this.selectedModel) {
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

      if (col) {
        col = this.camelCaseToDashCase(col);
        this.order = this.order === 'asc' ? 'desc' : 'asc'; // toggle order
        this.service.getAllSorted(col, this.order).subscribe({
          next: (response) => {
            this.response = response[responseItem];
            this.tableHeaders = this.response.length ? Object.keys(this.response[0]) : [];
            this.idColumnFirst();
          },
          error: (error) => {
            console.error(error || 'Could not fetch report')
          }
        })

      } else {
        this.service.getAllSorted().subscribe({
          next: (response) => {
            this.response = response[responseItem];
            this.tableHeaders = this.response.length ? Object.keys(this.response[0]) : [];
            this.idColumnFirst();
          },
          error: (error) => {
            console.error(error || 'Could not fetch report');
          }
        });
      }
    }
  }

  idColumnFirst() {
    // bring id col to far left
    const idIndex = this.tableHeaders.indexOf('id');
    if (idIndex !== 0) {
      this.tableHeaders.unshift(this.tableHeaders.splice(idIndex, 1)[0]);
    }
  }

  camelCaseToTitleCase(camelCaseString: string): string {
    return camelCaseString.replace(/([a-z])([A-Z])/g, '$1 $2').replace(/^./, (str) => str.toUpperCase());
  }

  camelCaseToDashCase(camelCaseString: string): string {
    return camelCaseString.replace(/([a-z])([A-Z])/g, '$1-$2').toLowerCase();
  }
}
