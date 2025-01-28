import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-sign-up',
  imports: [FormsModule],
  templateUrl: './sign-up.component.html',
  styleUrl: './sign-up.component.scss'
})

export class SignUpComponent {
  private apiUrl = 'http://localhost:5000/users'; // TODO variablize this later
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

    this.http.post<any>(this.apiUrl, signUpData).subscribe({
      next: (response) => {
        // clear an old error message
        this.successMessage = response.message;
        alert(this.successMessage);
        this.router.navigate(['/login']);
      },
      error: (error) => {
        // clear an old success message
        this.successMessage = '';
        this.errorMessage = error.error?.message || "Something went wrong";
      }
    });
  }
  
  goToLogin(): void {
    this.router.navigate(['/login']);
  }
}
