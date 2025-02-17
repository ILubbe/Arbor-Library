import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CancelReservationsComponent } from './cancel-reservations.component';

describe('CancelReservationsComponent', () => {
  let component: CancelReservationsComponent;
  let fixture: ComponentFixture<CancelReservationsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CancelReservationsComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CancelReservationsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
