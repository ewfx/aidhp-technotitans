import { TestBed } from '@angular/core/testing';

import { LoanRecommendationService } from './loan-recommendation.service';

describe('LoanRecommendationService', () => {
  let service: LoanRecommendationService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(LoanRecommendationService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
