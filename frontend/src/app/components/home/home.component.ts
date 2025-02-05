import { Component, OnInit } from '@angular/core';
import { Router, RouterModule } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { UserService } from '../../services/user.service';
import { SearchBarComponent } from '../search-bar/search-bar.component';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  imports: [RouterModule, SearchBarComponent],
  styleUrls: ['./home.component.scss']
})

export class HomeComponent implements OnInit {
  userFirstName: string = '';
  userLastName: string = '';
  userRole: string = '';
  isLibrarian: boolean = false;
  
  selectedModel: string = 'Book';
  selectedField: string = '';
  fieldOptions: string[] = ['author', 'title', 'genre', 'first_publish_year'];

  constructor(private router: Router, private authService: AuthService, private userService: UserService) {}

  ngOnInit(): void {
    const required_role = 'librarian';
    const userRole = this.authService.getUserRole();
    if(userRole === required_role){
      this.isLibrarian = true;
    }
    this.fetchUserProfile();
  }

  fetchUserProfile(): void {
    this.userService.getUserProfile().subscribe({
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

  logout() {
    this.authService.logout();
  }

  onSearchQueryEmitted(queryData: any) {
  }

  onFieldChange(field: any) {
  }
}