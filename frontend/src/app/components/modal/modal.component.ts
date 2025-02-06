import { Component, Input, Output, EventEmitter } from '@angular/core';
import { ReservationService } from '../../services/reservation.service';
import { UserService } from '../../services/user.service';
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
  @Input() isBookDetailsModal: boolean = false;
  @Input() isMyReservationsModal: boolean = false;
  @Input() isMyAccountModal: boolean = false;

  // general modal stuff
  @Input() showModal: boolean = false;
  @Input() modalTitle: string = '';
  @Output() closeModal = new EventEmitter<void>();

  // for specific things the modal does
  @Input() reservations: any = '';
  @Input() bookDetails: any = '';
  @Input() userDetails: any = '';

  // for updating user details in My Account Modal
  isEditMode: boolean = false;
  firstName: string = '';
  lastName: string = '';
  password: string = '';
  passwordConfirmation: string = '';

  constructor(
    private reservationService: ReservationService,
    private userService: UserService,
    private authService: AuthService
  ) {}

  createMyReservation(bookId: string) {
    if (!bookId) {
      console.log('Book ID is missing!');
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
      console.log('Reservation ID is missing!');
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

  cancelEdit() {
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
      this.authService.logout();
    }
  }

  close() {
    this.closeModal.emit();
  }
}