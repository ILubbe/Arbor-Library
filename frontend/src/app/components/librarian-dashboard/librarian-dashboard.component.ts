import { Component, OnInit } from '@angular/core';
import { Router, RouterModule } from '@angular/router';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-librarian-dashboard',
  imports: [RouterModule],
  templateUrl: './librarian-dashboard.component.html',
  styleUrl: './librarian-dashboard.component.scss'
})

export class LibrarianDashboardComponent implements OnInit {
  isLibrarian: boolean = false;
  
  constructor(private router: Router, private authService: AuthService ) {}

  ngOnInit(): void {
    const required_role = 'librarian';
    const userRole = this.authService.getUserRole();
    if(userRole === required_role){
      this.isLibrarian = true;
    }
  }
}
