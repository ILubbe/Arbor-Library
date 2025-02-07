import { Component } from '@angular/core';
import { CheckinComponent } from './checkin/checkin.component';
import { CheckoutComponent } from './checkout/checkout.component';

@Component({
  selector: 'app-checkin-checkout',
  imports: [CheckinComponent, CheckoutComponent],
  templateUrl: './checkin-checkout.component.html',
  styleUrl: './checkin-checkout.component.scss'
})
export class CheckinCheckoutComponent {
  showCheckin: boolean = false;
  showCheckout: boolean = false;

  constructor() {}
}
