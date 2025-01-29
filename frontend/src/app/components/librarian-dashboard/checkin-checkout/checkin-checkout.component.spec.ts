import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CheckinCheckoutComponent } from './checkin-checkout.component';

describe('CheckinCheckoutComponent', () => {
  let component: CheckinCheckoutComponent;
  let fixture: ComponentFixture<CheckinCheckoutComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CheckinCheckoutComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CheckinCheckoutComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
