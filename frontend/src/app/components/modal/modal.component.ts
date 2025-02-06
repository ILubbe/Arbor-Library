import { Component, Input, Output, EventEmitter } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { AuthService } from '../../services/auth.service';
import { environment } from '../../../environments/environment';

@Component({
  selector: 'app-modal',
  templateUrl: './modal.component.html',
  styleUrls: ['./modal.component.scss']
})
export class ModalComponent {
  // discover what page is using the modal
  @Input() isHomePage: boolean = false;

  @Input() showModal: boolean = false;
  @Input() modalTitle: string = '';
  @Input() modalContent: string = '';
  @Input() bookId: string = '';
  @Output() closeModal = new EventEmitter<void>();

  private apiReservationEndpoint = environment.backendUrl + '/reservations/my';

  constructor(private http: HttpClient, private authService: AuthService) {}

  onReserveBook() {
    if (!this.bookId) {
      console.log('Book ID is missing!');
      return;
    }

    const reservationData = {
      bookId: this.bookId
    };

    const accessToken = this.authService.getAccessToken();
    const headers = {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json'
    };

    this.http.post(this.apiReservationEndpoint, reservationData, { headers })
      .subscribe(
        (response) => {
          alert("Reservation Created!");
          this.closeModal.emit();
        },
        (error) => {
          alert(error.error.message);
        }
      );
    }

  close() {
    this.closeModal.emit();
  }
}