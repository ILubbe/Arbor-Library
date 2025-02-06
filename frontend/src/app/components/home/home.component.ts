import { Component, OnInit } from '@angular/core';
import { Router, RouterModule } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { UserService } from '../../services/user.service';
import { BookService } from '../../services/book.service';
import { ReservationService } from '../../services/reservation.service';
import { SearchBarComponent } from '../search-bar/search-bar.component';
import { ModalComponent } from '../modal/modal.component';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  imports: [RouterModule, SearchBarComponent, ModalComponent],
  styleUrls: ['./home.component.scss']
})

export class HomeComponent implements OnInit {
  isHomePage: boolean = true;
  isBookDetailsModal: boolean = false;
  selectedModel: string = 'Book'
  userFirstName: string = '';
  userLastName: string = '';
  userRole: string = '';
  isLibrarian: boolean = false;
  selectedField: string = '';
  fieldOptions: string[] = ['Author', 'Title', 'Genre', 'First Publish Year'];
  showModal: boolean = false;
  modalTitle: string = '';
  modalContent: string = '';
  bookId: string = '';
  selectedItem: any = null;
  reservations: any[] = [];

  constructor(
    private router: Router,
    private authService: AuthService,
    private userService: UserService,
    private bookService: BookService,
    private reservationService: ReservationService
  ) {}

  ngOnInit(): void {
    const required_role = 'librarian';
    const userRole = this.authService.getUserRole();
    if(userRole === required_role){
      this.isLibrarian = true;
    }
    this.fetchUserProfile();
  }

  fetchUserProfile(): void {
    this.userService.getUserProfile().subscribe({
      next: (response) => { // make first char uppercase for home page greeting
        this.userFirstName = response.user.firstName.charAt(0).toUpperCase() + response.user.firstName.slice(1);
        this.userLastName = response.user.lastName.charAt(0).toUpperCase() + response.user.lastName.slice(1);
        this.userRole = response.user.role.charAt(0).toUpperCase() + response.user.role.slice(1);
      },
      error: (error) => {
        console.error(error);
      }
    });
  }

  onSearchQueryEmitted(queryData: any) {
  }

  onFieldChange(field: any) {
  }

  onItemSelected(item: any) {
    this.isBookDetailsModal = true;
    this.selectedItem = item;
    this.modalContent = `
      <b>Title:</b> ${item.title}<br>
      <b>Author:</b> ${item.author}<br>
      <b>First Publish Year:</b> ${item.firstPublishYear}<br>
      <b>Genres:</b> ${item.genres.join(', ')}<br><br>`;
    this.bookId = item.id;
    this.showModal = true;
  }

  viewReservations() {
    this.isBookDetailsModal = false;
    this.reservationService.getMyReservations().subscribe({
      next: (response) => {
        this.reservations = response.reservations
        this.generateReservationsContent();
        this.showModal = true;
      },
      error: (error) => {
        alert(error);
      }
    });
  }

  generateReservationsContent(): void {
    const promises = this.reservations.map((reservation) => {
      return this.bookService.getBookById(reservation.bookId).toPromise().then((response) => {
        reservation.bookTitle = response.book.title;
        reservation.bookAuthor = response.book.author;
      }).catch((error) => {
        console.error('Error fetching book details:', error);
      });
    });
  }

  viewAccount() {

  }

  closeModal() {
    this.showModal = false;
    this.selectedItem = null;
    this.modalContent = '';
  }

  logout() {
    this.authService.logout();
  }
}