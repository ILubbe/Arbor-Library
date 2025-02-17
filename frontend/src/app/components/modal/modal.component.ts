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
  @Input() isReservationsPage: boolean = false;
  @Input() isBookDetailsModal: boolean = false;
  @Input() isUserDetailsModal: boolean = false;
  @Input() isMyReservationsModal: boolean = false;
  @Input() isMyAccountModal: boolean = false;
  @Input() isMyCheckoutsModal: boolean = false;
  @Input() isGenreModal: boolean = false;

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

  // for adding/editing a book
  title: string = '';
  author: string = '';
  firstPublishYear: number | null = null;
  genres: string[] = [];
  conditions: string[] = ['New', 'Good', 'Fair', 'Poor', 'Unknown'];
  bookCondition: string = 'Unknown';

  // for genre association
  allGenres: any[] = [];
  selectedGenres: Set<number> = new Set();
  associatedGenres: Set<number> = new Set();
  showGenres: boolean = false;
  perPage: number = 5;
  currentPage: number = 1;
  totalPages: number = 1;
  pagedGenres: any[] = [];

  // for creating a genre
  genreName: string = '';

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

  getGenres() {
    this.bookService.getGenres().subscribe({
      next: (response) => {
        this.allGenres = response.genres;
        if (this.bookDetails.id) {
          this.getAssociatedGenres(this.bookDetails.id).then(() => {
            this.paginateGenres();
            this.showGenres = true;
          });
        }
      },
      error: (error) => {
        console.error(error || "Error fetching genres")
      }
    });
  }

  paginateGenres() {
    const sortedGenres = [...this.allGenres].sort((a, b) => {
      const aSelected = this.selectedGenres.has(a.id) ? -1 : 1;
      const bSelected = this.selectedGenres.has(b.id) ? -1 : 1;
      return aSelected - bSelected || a.genre.localeCompare(b.genre);
    });

    const startIndex = (this.currentPage - 1) * this.perPage;
    const endIndex = startIndex + this.perPage;
    this.pagedGenres = sortedGenres.slice(startIndex, endIndex);
    this.totalPages = Math.ceil(this.allGenres.length / this.perPage);
  }

  nextPage() {
    if (this.currentPage * this.perPage < this.allGenres.length) {
      this.currentPage++;
      this.paginateGenres();
    }
  }
  
  prevPage() {
    if (this.currentPage > 1) {
      this.currentPage--;
      this.paginateGenres();
    }
  }

  getAssociatedGenres(bookId: string): Promise<void> {
    return new Promise((resolve) => {
      this.bookService.getAssociatedGenres(bookId).subscribe({
        next: (response) => {
          this.associatedGenres = new Set(response.genresByBook);
          this.selectedGenres = new Set(response.genresByBook);
          resolve();
        },
        error: (error) => {
          console.error(error || "Could not fetch associated genres")
        }
      });
    });
  }


  toggleGenreSelection(genreId: number): void {
    if (this.selectedGenres.has(genreId)) {
      this.selectedGenres.delete(genreId);
    } else {
      this.selectedGenres.add(genreId);
    }
  }

  closeGenres() {
    this.currentPage = 1;
    this.showGenres = false;
  }

  saveGenreSelection() {
    const selectedGenreIds = new Set(this.selectedGenres);
    const associatedGenreIds = new Set(this.associatedGenres);
  
    selectedGenreIds.forEach((genreId: number) => {
      if (this.bookDetails.id) {
        // ff genre is newly selected and wasn't previously associated, associate it
        if (!associatedGenreIds.has(genreId)) {
          this.bookService.associateBookToGenre(this.bookDetails.id, genreId).subscribe({
            next: (response) => {
              console.log(response || `Genre ID ${genreId} successfully associated to Book ID ${this.bookDetails.id}`);
            },
            error: (error) => {
              console.error(error || `Error associating Genre ID ${genreId} to Book ID ${this.bookDetails.id}`);
            }
          });
        }
      }
    });
  
    associatedGenreIds.forEach((genreId: number) => {
      // if genre was previously associated but is no longer selected, unassociate it
      if (!selectedGenreIds.has(genreId)) {
        this.bookService.unassociateBookToGenre(this.bookDetails.id, genreId).subscribe({
          next: (response) => {
            console.log(response || `Genre ID ${genreId} unassociated from Book ID ${this.bookDetails.id}`);
          },
          error: (error) => {
            console.error(error || `Error unassociating Genre ID ${genreId} from Book ID ${this.bookDetails.id}`);
          }
        });
      }
    });
    this.associatedGenres = new Set();
    this.closeGenres();
  }

  saveBook() { 
    if (this.modalTitle.includes("Edit")) {
      const updatedBookDetails = {
        title: this.bookDetails.title,
        author: this.bookDetails.author,
        firstPublishYear: this.bookDetails.firstPublishYear,
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

    } else {
      const newBookDetails = {
        title: this.title,
        author: this.author,
        firstPublishYear: this.firstPublishYear,
        genres: this.genres,
        bookCondition: this.bookCondition
      };

      this.bookService.addBook(newBookDetails).subscribe({
        next: (response) => {
          alert(response.message || 'Book added successfully');
          this.close();
        },
        error: (error) => {
          alert(error);
        }
      });
      // reset these for the next new modal.
      this.title = '';
      this.author = '';
      this.firstPublishYear = null;
      this.genres = [];
      this.bookCondition = 'Unknown';
    }
  }

  saveGenre() {
    this.bookService.addGenre(this.genreName).subscribe({
      next: (response) => {
        alert(response.message || 'Genre added successfully');
        this.close();
      },
      error: (error) => {
        alert(error);
      }
    });
    // reset these for the next new modal
    this.isGenreModal = false;
  }

  close() {
    this.closeGenres();
    this.closeModal.emit();
  }
}