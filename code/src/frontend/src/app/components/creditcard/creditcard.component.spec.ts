import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreditCardComponent } from './creditcard.component';

describe('CreditcardComponent', () => {
  let component: CreditCardComponent;
  let fixture: ComponentFixture<CreditCardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CreditCardComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CreditCardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
