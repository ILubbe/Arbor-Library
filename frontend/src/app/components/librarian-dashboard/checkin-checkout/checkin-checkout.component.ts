import { Component } from '@angular/core';
import { OutComponent } from './out/out.component';
import { InComponent } from './in/in.component';

@Component({
  selector: 'app-checkin-checkout',
  imports: [InComponent, OutComponent],
  templateUrl: './checkin-checkout.component.html',
  styleUrl: './checkin-checkout.component.scss'
})
export class CheckinCheckoutComponent {
  showCheckin: boolean = false;
  showCheckout: boolean = false;

  constructor() {}
}
