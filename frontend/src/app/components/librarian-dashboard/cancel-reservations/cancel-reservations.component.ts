import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ReservationService } from '../../../services/reservation.service';
import { SearchBarComponent } from '../../search-bar/search-bar.component';
import { ModalComponent } from '../../modal/modal.component';

@Component({
  selector: 'app-cancel-reservations',
  imports: [FormsModule, SearchBarComponent, ModalComponent],
  templateUrl: './cancel-reservations.component.html',
  styleUrl: './cancel-reservations.component.scss'
})

export class CancelReservationsComponent {
  // give search bar component context it needs
  isReservationsPage: boolean = true;
  isUserSearch: boolean = true;
  isBookSearch: boolean = true;
  isReservationsSearch: boolean = false;
  selectedUserModel: string = 'User';
  selectedBookModel: string = 'Book';
  selectedReservationModel: string = 'Reservation';
  perPage: number = 5;

  // toggle User/Book search bars
  isUserSearchVisible: boolean = true;

  // for field select drop down
  fieldUserOptions: string[] = ['Email', 'First Name', 'Last Name', 'Role'];
  fieldBookOptions: string[] = ['Author', 'Title', 'Genre', 'First Publish Year'];
  selectedUserField: string = '';
  selectedBookField: string = '';

  // search result selection
  userId: string = '';
  bookId: string = '';
  reservationId: string = '';

  // for giving modal component context
  isBookDetailsModal: boolean = false;
  isUserDetailsModal: boolean = false;

  // general modal stuff
  showModal: boolean = false;
  modalTitle: string = '';
  selectedItem: any = null;

  // for book Details modal with search results
  bookDetails: any = '';

  // for user details modal with search results
  userDetails: any = '';

  constructor(private reservationService: ReservationService) {}

  onUserItemSelected(item: any) {
    if (!this.userId) {
      this.userId = item.id;
    } else {
      this.reservationId = item.id;
    }
  }

  onBookItemSelected(item: any) {
    if (!this.bookId) {
      this.bookId = item.id;
    } else {
      this.reservationId = item.id;
    }
  }

  toggleSearchType() {
    this.clear();
    this.isUserSearchVisible = !this.isUserSearchVisible;
  }

  clear() {
    this.userId = '';
    this.bookId = '';
    this.reservationId = '';
  }

  cancelReservation() {
    if (!this.reservationId) {
      alert('Reservation ID must be provided!');
      return;
    }

    this.reservationService.cancelReservation(this.reservationId).subscribe({
      next: (response) => {
        alert(response.message || 'Reservation successfully canceled!');
        window.scrollTo(0, 0);
      },
      error: (error) => {
        alert(error || 'Could not cancel reservation');
        window.scrollTo(0, 0);
      }
    });
    this.clear();
  }

  onUserDetailsReceived(user: any) {
    this.isBookDetailsModal = false;
    this.isUserDetailsModal = true;
    this.userDetails = user;
    this.modalTitle = 'User Details';
    this.showModal = true;
  }
  
  onBookDetailsReceived(book: any) {
    this.isUserDetailsModal = false;
    this.isBookDetailsModal = true;
    this.bookDetails = book;
    this.modalTitle = 'Book Details';
    this.showModal = true;
  }

  closeModal() {
    this.showModal = false;
  }
}
