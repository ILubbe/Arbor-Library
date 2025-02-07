import { TestBed } from '@angular/core/testing';

import { CheckinCheckoutService } from './checkin-checkout.service';

describe('CheckinCheckoutService', () => {
  let service: CheckinCheckoutService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(CheckinCheckoutService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
