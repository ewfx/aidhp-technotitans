import { Component, OnInit } from '@angular/core';
import { LoanRecommendationService } from '../../services/loan-recommendation.service';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { NavbarComponent } from '../navbar/navbar.component';
import { ChatbotComponent } from '../chatbot/chatbot.component';

interface Loan {
  loan_type: string;
  benefits: string;
  special_offers: string;
  processing_time: string;
}

@Component({
  selector: 'app-loans',
  standalone: true,
  imports: [CommonModule, HttpClientModule, NavbarComponent,ChatbotComponent], // ✅ Ensure HttpClientModule is imported
  templateUrl: './loans.component.html',
  styleUrls: ['./loans.component.scss'],
  providers: [LoanRecommendationService], // ✅ Provide the service
})
export class LoansComponent implements OnInit {
  recommendations: Loan[] = [];
  loading: boolean = false;
  error: string = '';
  userId: string | null = '';

  constructor(private loanService: LoanRecommendationService) {}

  ngOnInit(): void {
    this.userId = localStorage.getItem('customerId'); // ✅ Get user ID dynamically
    this.fetchLoanRecommendations();
  }


  fetchLoanRecommendations() {
    this.loading = true;
    this.error = '';
    this.recommendations = [];

    this.loanService.getLoanRecommendation(this.userId).subscribe({
      next: (response) => {
        console.log('API Response:', response); // ✅ Debugging the response

        if (!response || !response.loans) {
          this.error = 'Unexpected response format.';
          console.error('API Error:', response);
          return;
        }

        this.recommendations = response.loans; // ✅ No need for `raw_response` cleaning
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Failed to fetch loan recommendations.';
        console.error('HTTP Error:', err);
        this.loading = false;
      },
    });
  }
}
