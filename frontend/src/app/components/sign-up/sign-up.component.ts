import { Component } from '@angular/core';
import { Router, RouterModule } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { environment } from '../../../environments/environment';

@Component({
  selector: 'app-sign-up',
  imports: [FormsModule, RouterModule],
  templateUrl: './sign-up.component.html',
  styleUrl: './sign-up.component.scss'
})

export class SignUpComponent {
  private apiEndpoint = environment.backendUrl + 'users';
  email: string = '';
  password: string = '';
  passwordConfirmation: string = '';
  firstName: string = '';
  lastName: string = '';
  errorMessage: string = '';
  successMessage: string = '';
  constructor(private http: HttpClient, private router: Router) { }

  onSubmit(): void {
    const signUpData = {
      email: this.email,
      password: this.password,
      passwordConfirmation: this.passwordConfirmation,
      firstName: this.firstName,
      lastName: this.lastName
    };

    this.http.post<any>(this.apiEndpoint, signUpData).subscribe({
      next: (response) => {
        // clear an old error message
        this.successMessage = response.message;
        alert(this.successMessage);
        this.router.navigateByUrl('/login');
      },
      error: (error) => {
        // clear an old success message
        this.successMessage = '';
        this.errorMessage = error.error?.message || "Something went wrong";
      }
    });
  }
}
