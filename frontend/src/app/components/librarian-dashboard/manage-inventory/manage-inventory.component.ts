import { Component, ViewChild } from '@angular/core';
import { BookService } from '../../../services/book.service';
import { SearchBarComponent } from '../../search-bar/search-bar.component';
import { ModalComponent } from '../../modal/modal.component';

@Component({
  selector: 'app-manage-inventory',
  imports: [SearchBarComponent, ModalComponent],
  templateUrl: './manage-inventory.component.html',
  styleUrl: './manage-inventory.component.scss'
})
export class ManageInventoryComponent {
  // for giving modal component context
  isInventoryPage: boolean = true;
  isBookDetailsModal: boolean = false;

  // for search
  isBookSearch: boolean = true;
  selectedModel: string = 'Book'
  selectedField: string = '';
  fieldOptions: string[] = ['Author', 'Title', 'Genre', 'First Publish Year', 'Book Condition'];

  // general modal stuff
  showModal: boolean = false;
  modalTitle: string = '';
  selectedItem: any = null;

  // for book Details modal with search results
  bookDetails: any[] = [];

  @ViewChild(SearchBarComponent) searchBar!: SearchBarComponent;

  constructor(private bookService: BookService) {}

  addBook() {
    this.isBookDetailsModal = true;
    this.bookDetails = [];
    this.modalTitle = 'Add Book';
    this.showModal = true;
  }

  onItemSelected(item: any) {
    this.isBookDetailsModal = true;
    this.selectedItem = item;
    this.modalTitle = 'Edit Book';
    this.bookService.getBookById(this.selectedItem).subscribe({
      next: (response) => {
        this.bookDetails = response.book;
        this.showModal = true;
      },
      error: (error) => {
        alert(error || 'Failed to load book details');
      }
    });
  }

  closeModal() {
    this.showModal = false;
    this.modalTitle = '';
    this.selectedItem = null;
    if (this.searchBar) {
      this.searchBar.onQueryChange(this.searchBar.query); // refreshed search so librarian can see changes
    }
  }
}
