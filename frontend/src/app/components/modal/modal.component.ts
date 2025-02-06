import { Component, Input, Output, EventEmitter } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { AuthService } from '../../services/auth.service';
import { ReservationService } from '../../services/reservation.service';

@Component({
  selector: 'app-modal',
  templateUrl: './modal.component.html',
  styleUrls: ['./modal.component.scss']
})
export class ModalComponent {
  // discover what page is using the modal
  @Input() isHomePage: boolean = false;
  @Input() isBookDetailsModal: boolean = false;
  @Input() isMyReservationsModal: boolean = false;

  @Input() showModal: boolean = false;
  @Input() modalTitle: string = '';
  @Input() modalContent: string = '';
  @Input() reservations: any = '';
  @Input() bookId: string = '';
  @Output() closeModal = new EventEmitter<void>();

  constructor(private http: HttpClient, private authService: AuthService, private reservationService: ReservationService) {}

  createMyReservation() {
    if (!this.bookId) {
      console.log('Book ID is missing!');
      return;
    }

    this.reservationService.createMyReservation(this.bookId).subscribe({
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
      console.log('Reservation ID is missing!');
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

  close() {
    this.closeModal.emit();
  }
}