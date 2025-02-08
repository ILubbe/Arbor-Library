import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CheckinCheckoutService } from '../../../../services/checkin-checkout.service';
import { SearchBarComponent } from '../../../search-bar/search-bar.component';
import { ModalComponent } from '../../../modal/modal.component';

@Component({
  selector: 'app-in',
  imports: [FormsModule, SearchBarComponent, ModalComponent],
  templateUrl: './in.component.html',
  styleUrl: './in.component.scss'
})

export class InComponent {
  // give search bar component context it needs
  isCheckinPage: boolean = true;
  isUserSearch: boolean = true;
  isBookSearch: boolean = true;
  isCheckoutSearch: boolean = false;
  selectedUserModel: string = 'User';
  selectedBookModel: string = 'Book';
  selectedCheckoutModel: string = 'Checkout';
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
  checkoutId: string = '';

  // for giving modal component context
  isBookDetailsModal: boolean = false;
  isUserDetailsModal: boolean = false;

  // general modal stuff
  showModal: boolean = false;
  modalTitle: string = '';
  selectedItem: any = null;

  // for book Details modal with search results
  bookDetails: any = '';

  // for user details modal
  userDetails: any = '';

  constructor(private ciCoService: CheckinCheckoutService) {}

  onUserItemSelected(item: any) {
    if (!this.userId) {
      this.userId = item.id;
    } else {
      this.checkoutId = item.id;
    }
  }

  onBookItemSelected(item: any) {
    if (!this.bookId) {
      this.bookId = item.id;
    } else {
      this.checkoutId = item.id;
    }
  }

  toggleSearchType() {
    this.clear();
    this.isUserSearchVisible = !this.isUserSearchVisible;
  }

  clear() {
    this.userId = '';
    this.bookId = '';
    this.checkoutId = '';
  }

  checkinBook() {
    if (!this.checkoutId) {
      alert('Checkout ID must be provided!');
      return;
    }

    this.ciCoService.checkin(this.checkoutId).subscribe({
      next: (response) => {
        alert(response.message || 'Book successfully checked in!');
        window.scrollTo(0, 0);
      },
      error: (error) => {
        alert(error || 'Could not check in book');
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
