import { Component, Input, Output, EventEmitter } from '@angular/core';
import { Router } from '@angular/router';
import { ReservationService } from '../../services/reservation.service';
import { UserService } from '../../services/user.service';
import { BookService } from '../../services/book.service';
import { AuthService } from '../../services/auth.service';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-modal',
  templateUrl: './modal.component.html',
  imports: [FormsModule],
  styleUrls: ['./modal.component.scss']
})
export class ModalComponent {
  // discover what page is using the modal
  @Input() isHomePage: boolean = false;
  @Input() isCheckinPage: boolean = false;
  @Input() isInventoryPage: boolean = false;
  @Input() isBookDetailsModal: boolean = false;
  @Input() isUserDetailsModal: boolean = false;
  @Input() isMyReservationsModal: boolean = false;
  @Input() isMyAccountModal: boolean = false;
  @Input() isMyCheckoutsModal: boolean = false;

  // general modal stuff
  @Input() showModal: boolean = false;
  @Input() modalTitle: string = '';
  @Output() closeModal = new EventEmitter<void>();

  // for specific things the modal does
  @Input() reservations: any = '';
  @Input() bookDetails: any = '';
  @Input() userDetails: any = '';
  @Input() checkouts: any = '';

  // for updating user details in My Account
  isEditMode: boolean = false;
  firstName: string = '';
  lastName: string = '';
  password: string = '';
  passwordConfirmation: string = '';

  constructor(
    private reservationService: ReservationService,
    private userService: UserService,
    private authService: AuthService,
    private bookService: BookService,
    private router: Router
  ) {}

  createMyReservation(bookId: string) {
    if (!bookId) {
      alert('Book ID is missing!');
      return;
    }

    this.reservationService.createMyReservation(bookId).subscribe({
      next: (response) => {
        alert(response.message);
      },
      error: (error) => {
        alert(error);
      }
    });
    this.close();
  }

  cancelMyReservation(reservationId: string) {
    if (!reservationId) {
      alert('Reservation ID is missing!');
      return;
    }
    this.reservationService.cancelMyReservation(reservationId).subscribe({
      next: (response) => {
        alert(response.message);
      },
      error: (error) => {
        alert(error);
      }
    });
    this.close();
  }

  editMyAccount() {
    this.isEditMode = true;
    this.firstName = this.userDetails.firstName;
    this.lastName = this.userDetails.lastName;
    this.password = this.userDetails.password;
    this.passwordConfirmation = this.userDetails.passwordConfirmation;
  }

  saveMyAccount() {
    const updatedUserDetails = {
      firstName: this.firstName,
      lastName: this.lastName,
      password: this.password,
      passwordConfirmation: this.passwordConfirmation
    };

    this.userService.updateMyProfile(updatedUserDetails).subscribe({
      next: (response) => {
        alert(response.message || 'Account updated successfully');
        this.authService.logout()
        this.isEditMode = false; // switch back to view mode
      },
      error: (error) => {
        this.firstName = this.userDetails.firstName;
        this.lastName = this.userDetails.lastName;
        alert(error);
      }
    });
  }

  cancelMyAccountEdit() {
    this.isEditMode = false;
    this.firstName = this.userDetails.firstName;
    this.lastName = this.userDetails.lastName;
  }

  deleteMyAccount() {
    const isConfirmed = confirm('Are you sure you want to delete your account?');
    if (isConfirmed) {
      this.userService.deleteMyProfile().subscribe({
        next: (response) => {
          alert(response.message || 'Your account has been deleted')
        },
        error: (error) => {
          alert(error || 'Failed to delete account');
        }
      });
      // cant call this function because backend doesn't like to log out a user who doesn't exist anymore.
      // this.authService.logout();
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
      this.router.navigateByUrl('/login');
    }
  }

  saveBookEdit() {
    const updatedBookDetails = {
      title: this.bookDetails.title,
      author: this.bookDetails.author,
      firstPublishYear: this.bookDetails.firstPublishYear,
      genres: this.bookDetails.genres,
      bookCondition: this.bookDetails.bookCondition
    };

    this.bookService.updateBook(this.bookDetails.id, updatedBookDetails).subscribe({
      next: (response) => {
        alert(response.message || 'Book updated successfully');
        this.close();
      },
      error: (error) => {
        alert(error);
      }
    });
  }

  cancelBookEdit() {
    this.close();
  }

  close() {
    this.closeModal.emit();
  }
}