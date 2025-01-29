import { Component } from '@angular/core';
import { Router, RouterModule } from '@angular/router';

@Component({
  selector: 'app-librarian-dashboard',
  imports: [RouterModule],
  templateUrl: './librarian-dashboard.component.html',
  styleUrl: './librarian-dashboard.component.scss'
})
export class LibrarianDashboardComponent {
  constructor(private router: Router) {}
}
