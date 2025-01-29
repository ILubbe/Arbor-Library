import { Component, OnInit } from '@angular/core';
import { jwtDecode } from 'jwt-decode';
import { Router, RouterModule } from '@angular/router';
import { UserService } from '../../services/user.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  imports: [RouterModule],
  styleUrls: ['./home.component.scss']
})

export class HomeComponent implements OnInit {
  userFirstName: string = '';
  userLastName: string = '';
  userRole: string = '';
  isLibrarian: boolean = false;

  constructor(private router: Router, private userService: UserService) {}

  ngOnInit(): void {
    this.checkUserRole();
    this.fetchUserProfile();
  }

  checkUserRole() {
    const accessToken = localStorage.getItem('accessToken');
    if (accessToken) {
      try {
        const decodedToken: any = jwtDecode(accessToken);
        // Check if the token contains the 'role' property and it's 'librarian'
        if (decodedToken.role === 'librarian') {
          this.isLibrarian = true;
        }
      } catch (error) {
        console.error('Error decoding token', error);
      }
    }
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
}