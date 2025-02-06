import { Component, Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-modal',
  templateUrl: './modal.component.html',
  styleUrls: ['./modal.component.scss']
})
export class ModalComponent {
  @Input() showModal: boolean = false;
  @Input() modalTitle: string = '';
  @Input() modalContent: string = '';
  @Output() closeModal = new EventEmitter<void>();

  close() {
    this.closeModal.emit();  // Emit event to close the modal
  }
}