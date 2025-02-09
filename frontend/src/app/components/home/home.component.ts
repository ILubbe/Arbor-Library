import { Component, OnInit } from '@angular/core';
import { RouterModule } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { UserService } from '../../services/user.service';
import { BookService } from '../../services/book.service';
import { ReservationService } from '../../services/reservation.service';
import { CheckinCheckoutService } from '../../services/checkin-checkout.service';
import { SearchBarComponent } from '../search-bar/search-bar.component';
import { ModalComponent } from '../modal/modal.component';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  imports: [RouterModule, SearchBarComponent, ModalComponent],
  styleUrls: ['./home.component.scss']
})

export class HomeComponent implements OnInit {
  // for giving modal component context
  isHomePage: boolean = true;
  isBookDetailsModal: boolean = false;
  isMyReservationsModal: boolean = false;
  isMyAccountModal: boolean = false;
  isMyCheckoutsModal: boolean = false;

  // for search
  isBookSearch: boolean = true;
  selectedModel: string = 'Book'
  selectedField: string = '';
  fieldOptions: string[] = ['Author', 'Title', 'Genre', 'First Publish Year'];

  // general modal stuff
  showModal: boolean = false;
  modalTitle: string = '';
  selectedItem: any = null;

  // for greeting & library dashboard button
  userFirstName: string = '';
  userLastName: string = '';
  userRole: string = '';
  isLibrarian: boolean = false;

  // for book Details modal with search results
  bookDetails: any = '';

  // for My Reservations modal
  reservations: any[] = [];

  // for My Account modal
  userDetails: any = '';

  // for My Checkouts modal
  checkouts: any[] = [];

  constructor(
    private authService: AuthService,
    private userService: UserService,
    private bookService: BookService,
    private reservationService: ReservationService,
    private ciCoService: CheckinCheckoutService
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
    this.userService.getMyProfile().subscribe({
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

  onItemSelected(item: any) {
    this.isMyReservationsModal = false;
    this.isMyAccountModal = false;
    this.isMyCheckoutsModal = false;
    this.isBookDetailsModal = true;
    this.selectedItem = item;
    this.modalTitle = 'Book Details';
    this.bookService.getBookById(this.selectedItem.id).subscribe({
      next: (response) => {
        this.bookDetails = response.book;
        this.showModal = true;
      },
      error: (error) => {
        alert(error || 'Failed to load book details');
      }
    });
  }

  viewReservations() {
    this.isBookDetailsModal = false;
    this.isMyAccountModal = false;
    this.isMyCheckoutsModal = false;
    this.isMyReservationsModal = true;
    this.modalTitle = 'My Reservations';
    this.reservationService.getMyReservations().subscribe({
      next: (response) => {
        this.reservations = response.reservations
        // add book details that reservations db table doesn't hold
        this.generateReservationsContent();
        this.showModal = true;
      },
      error: (error) => {
        alert(error);
      }
    });
  }

  generateReservationsContent(): void {
    this.reservations.map((reservation) => {
      return this.bookService.getBookById(reservation.bookId).toPromise()
      .then((response) => {
        reservation.bookTitle = response.book.title;
        reservation.bookAuthor = response.book.author;
      }).catch((error) => {
        console.error(error || 'Failed to fetch book details for reservations');
      });
    });
  }

  viewAccount() {
    this.isMyReservationsModal = false;
    this.isBookDetailsModal = false;
    this.isMyCheckoutsModal = false;
    this.isMyAccountModal = true;
    this.modalTitle = 'My Account';
    this.userService.getMyProfile().subscribe({
      next: (response) => {
        this.userDetails = response.user;
        this.showModal = true;
      },
      error: (error) => {
        alert(error || 'Failed to load user details');
      }
    });
  }

  viewCheckouts() {
    this.isMyReservationsModal = false;
    this.isBookDetailsModal = false;
    this.isMyAccountModal = false;
    this.isMyCheckoutsModal = true;
    this.modalTitle = 'My Check Outs'
    this.ciCoService.getMyCheckouts().subscribe({
      next: (response) => {
        this.checkouts = response.checkouts;
        // add book details that checkouts db table doesn't hold
        this.generateCheckoutsContent();
        this.showModal = true;
      },
      error: (error) => {
        alert(error || 'Failed to load user checkouts')
      }
    });
  }

  generateCheckoutsContent(): void {
    this.checkouts.map((checkout) => {
      return this.bookService.getBookById(checkout.bookId).toPromise()
      .then((response) => {
        checkout.bookTitle = response.book.title;
        checkout.bookAuthor = response.book.author;
      }).catch((error) => {
        console.error(error || 'Failed to fetch book details for checkouts');
      });
    });
  }

  closeModal() {
    this.showModal = false;
    this.selectedItem = null;
    this.modalTitle = '';
  }

  logout() {
    this.authService.logout();
  }
}