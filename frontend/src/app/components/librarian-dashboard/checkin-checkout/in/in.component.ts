import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CheckinCheckoutService } from '../../../../services/checkin-checkout.service';
import { SearchBarComponent } from '../../../search-bar/search-bar.component';

@Component({
  selector: 'app-in',
  imports: [FormsModule, SearchBarComponent],
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

  onCheckoutIdInput(item: any) {
    this.checkoutId = item;
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
}
