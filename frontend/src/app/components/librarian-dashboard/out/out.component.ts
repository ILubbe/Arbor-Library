import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CheckinCheckoutService } from '../../../services/checkin-checkout.service';
import { SearchBarComponent } from '../../search-bar/search-bar.component';

@Component({
  selector: 'app-out',
  imports: [FormsModule, SearchBarComponent],
  templateUrl: './out.component.html',
  styleUrl: './out.component.scss'
})

export class OutComponent {
  isCheckoutPage: boolean = true;
  isUserSearch: boolean = true;
  isBookSearch: boolean = true;
  perPage: number = 5;
  selectedUserModel: string = 'User';
  selectedBookModel: string = 'Book';
  fieldUserOptions: string[] = ['Email', 'First Name', 'Last Name', 'Role'];
  fieldBookOptions: string[] = ['Author', 'Title', 'Genre', 'First Publish Year'];
  selectedUserField: string = '';
  selectedBookField: string = '';
  userId: string = '';
  bookId: string = '';

  constructor(private ciCoService: CheckinCheckoutService) {}

  onUserItemSelected(item: any) {
    this.userId = item.id;
  }

  onBookItemSelected(item: any) {
    this.bookId = item.id;
  }

  checkoutBook() {
    if (!this.userId || !this.bookId) {
      alert('Both User ID and Book ID must be provided!');
      return;
    }

    this.ciCoService.checkout(this.userId, this.bookId).subscribe({
      next: (response) => {
        alert(response.message || 'Book successfully checked out!');
        this.userId = '';
        this.bookId = '';
        window.scrollTo(0, 0);
      },
      error: (error) => {
        alert(error || 'Could not check out book');
        window.scrollTo(0, 0);
      }
    });
  }
}
