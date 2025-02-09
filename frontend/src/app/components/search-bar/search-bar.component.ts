import { Component, Input, Output, EventEmitter } from '@angular/core';
import { AuthService } from '../../services/auth.service';
import { BookService } from '../../services/book.service';
import { UserService } from '../../services/user.service';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../environments/environment';
import { debounceTime, switchMap } from 'rxjs/operators';
import { Subject } from 'rxjs';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';

interface SearchResult {
  total: number;
  page: number;
  per_page: number;
  results: any[];
}

@Component({
  selector: 'app-search-bar',
  imports: [FormsModule],
  templateUrl: './search-bar.component.html',
  styleUrl: './search-bar.component.scss'
})
export class SearchBarComponent {
  // discover what page is using the search bar
  @Input() isHomePage: boolean = false;
  @Input() isCheckoutPage: boolean = false;
  @Input() isCheckinPage: boolean = false;
  @Input() isUserPage: boolean = false;

  // discover how this page will use the search bar
  @Input() isBookSearch: boolean = false;
  @Input() isUserSearch: boolean = false;
  @Input() isCheckoutSearch: boolean = false;

  // general searchbar inputs
  @Input() fieldOptions: string[] = [];
  @Input() selectedModel: string = '';
  @Input() selectedField: string = '';
  @Input() perPage: number = 25

  @Output() searchQuery = new EventEmitter<any>();
  @Output() itemSelected = new EventEmitter<any>();
  @Output() userSelected = new EventEmitter<any>();
  @Output() bookSelected = new EventEmitter<any>();

  query: string = '';
  page: number = 1;
  results: any[] = [];
  total: number = 0;

  lockedQuery: string = '';
  lockedField: string = '';

  // user specific search
  userId: string = '';

  // book specific search
  bookId: string = '';

  // checkout specific search
  checkoutId: string = '';

  private searchSubject = new Subject<string>;

  constructor(
    private http: HttpClient,
    private router: Router,
    private authService: AuthService,
    private bookService: BookService,
    private userService: UserService
  ) { 
    
    this.searchSubject.pipe(
      debounceTime(500),  // wait for 500ms after the user stops typing
      switchMap((query: string) => this.search(query))  // call search when the user stops typing
    ).subscribe((response: SearchResult) => {
      this.results = response.results;
      this.total = response.total;
      if (this.isCheckoutSearch) {
        this.results = this.results.filter(result => result.returned === false);
        this.total = this.results.length;
      }
      this.page = response.page;
      this.perPage = response.per_page;
    });
  }

  search(query: string) {
    if (this.isCheckoutSearch) {
      this.perPage = 10000; // set this as there will be no pagination on checkout searches due to filtering in template
    }
    let apiSearchEndpoint = environment.backendUrl + `/search?model=${this.selectedModel}&query=${this.query}&page=${this.page}&limit=${this.perPage}`;
    if (this.selectedField) {
      apiSearchEndpoint += `&field=${this.selectedField.replace(/ /g,'-')}`;
    }
    return this.authService.addHttpHeaders().pipe(
      switchMap((headers) => {
        return this.http.get<SearchResult>(apiSearchEndpoint, { headers });
      })
    )
  }

  onQueryChange(query: string) {
    if (this.query !== this.lockedQuery) {
      this.page = 1;
      this.lockedQuery = this.query; // lock the query
    }
    this.searchSubject.next(query);
    this.searchQuery.emit({
      model: this.selectedModel,
      field: this.selectedField,
      page: this.page,
      limit: this.perPage
    });
  }

  onFieldChange(field: string) {
    this.selectedField = field;
    if (this.selectedField !== this.lockedField) {
      this.page = 1;
      this.lockedField = this.selectedField; // lock the field
    }

    this.onQueryChange(this.query);
  }

  changePage(page: number) {
    this.page = page;
    this.onQueryChange(this.query);
    window.scrollTo(0, 0)
  }

  get totalPages(): number {
    return Math.ceil(this.total / this.perPage);
  }

  onViewDetailsClick(item: any) {
    this.itemSelected.emit(item);
  }

  onGetBookDetails(bookId: string) {
    this.bookService.getBookById(bookId).subscribe({
      next: (response) => {
        this.bookSelected.emit(response.book);
      },
      error: (error) => {
        alert(error || 'Failed to load book details');
      }
    });
  }

  onGetUserDetails(userId: string) {
    this.userService.getUserById(userId).subscribe({
      next: (response) => {
        this.userSelected.emit(response.user);
      },
      error: (error) => {
        alert(error || 'Failed to load user details');
      }
    });
  }

  onUserRoleToggle(userId: string) {
    this.userService.getMyProfile().subscribe({
      next: (response) => {
        if (response.user.id == userId) { // gotta warn if they're going to change their own role
          const changeOwnRoleConfirmed = confirm('WARNING: You are attempting to change your own role. You will no longer be able to access the librarian-dashboard.')
          if (changeOwnRoleConfirmed) {
            this.userService.SwitchUserRoleById(userId).subscribe({
              next: (response) => {
                alert(response.message || 'User role changed');
                this.authService.logout();
              },
              error: (error) => {
                alert(error || 'Failed to switch user role');
              }
            });
          }
        } else {
          this.userService.SwitchUserRoleById(userId).subscribe({
            next: (response) => {
              alert(response.message || 'User role changed');
              this.onQueryChange(this.query); // refresh search so librarian can see change
            },
            error: (error) => {
              alert(error || 'Failed to switch user role');
            }
          });
        }
      },
      error: (error) => {
        alert(error || 'Failed to fetch logged in user profile');
      }
    });
  }

  onUserDelete(userId: string) {
    const isConfirmed = confirm('Are you sure you want to delete this user?');
    if (isConfirmed) {
      this.userService.getMyProfile().subscribe({
        next: (response) => {
          if (response.user.id == userId) { // gotta warn if they're going to delete themselves
            const deleteYourselfConfirmed = confirm('WARNING: You are attempting to delete your own profile');
            if (deleteYourselfConfirmed) {
              this.userService.deleteUserById(userId).subscribe({
                next: (response) => {
                  alert(response.message || 'User deleted');
                  // cant call this function because backend doesn't like to log out a user who doesn't exist anymore.
                  // this.authService.logout();
                  localStorage.removeItem('accessToken');
                  localStorage.removeItem('refreshToken');
                  this.router.navigateByUrl('/login');
                },
                error: (error) => {
                  alert(error || 'Failed to delete user');
                }
              });
            }
          } else {
            this.userService.deleteUserById(userId).subscribe({
              next: (response) => {
                alert(response.message || 'User deleted');
                this.onQueryChange(this.query); // refresh search so librarian can see change
              },
              error: (error) => {
                alert(error || 'Failed to delete user');
              }
            });
          }
        },
        error: (error) => {
          alert(error || 'Failed to fetch logged in user profile');
        }
      });
    }
  }

  onSelectClick(item: any) {
    if (this.isUserSearch) {
      this.userId = item.id;
      this.itemSelected.emit(item);

      // send userId to checkout search if on check in page
      if (this.isCheckinPage) {
        this.isUserSearch = false;
        this.isCheckoutSearch = true;
        this.selectedModel = 'Checkout';
        this.selectedField = 'user-id';
        this.query = this.userId;
        this.onQueryChange(this.query);
      }
      
    } else if (this.isBookSearch) {
      this.bookId = item.id;
      this.itemSelected.emit(item);

      // send bookId to checkout search if on check in page
      if (this.isCheckinPage) {
        this.isBookSearch = false;
        this.isCheckoutSearch = true;
        this.selectedModel = 'Checkout';
        this.selectedField = 'book-id';
        this.query = this.bookId;
        this.onQueryChange(this.query);
      }

    } else if (this.isCheckoutSearch) {
      this.checkoutId = item.id;
      this.itemSelected.emit(item);
      this.isCheckoutSearch = false;
      this.clearResults();
    }
  }

  clearResults() {
    this.results = [];
    this.total = 0;
    this.page = 1;
    this.query = '';
  }
}
