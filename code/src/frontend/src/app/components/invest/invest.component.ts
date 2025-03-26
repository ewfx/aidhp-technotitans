import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { ChatbotComponent } from '../chatbot/chatbot.component';
import { NavbarComponent } from "../navbar/navbar.component";
import { FormsModule } from '@angular/forms'; 

@Component({
  selector: 'app-creditcard',
  imports: [CommonModule, ChatbotComponent, FormsModule, NavbarComponent],
  templateUrl: './invest.component.html',
  styleUrls: ['./invest.component.scss']
})

export class InvestComponent implements OnInit {
  creditCardRecommendation: any;
  selectedRisk: string = 'medium';  // Default dropdown value for risk
  selectedTenure: number = 1;       // Default tenure value
  isLoading: boolean = false;       // Tracks the loading state
  customerId: string | null = '';

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    this.customerId = localStorage.getItem('customerId'); // Fetch customerId from localStorage
  }

  searchRecommendations(): void {
    console.log("hihi");
    if (this.selectedTenure < 1 || this.selectedTenure > 40) {
      console.warn('Tenure must be between 1 and 40 years.');
      alert('Please enter a valid tenure between 1 and 40 years.');
      return;
    }

    const requestData = {
      risk: this.selectedRisk,
      tenure: this.selectedTenure,
    };

    this.isLoading = true; // Set loading state to true while waiting for response

    // Make the POST request to the backend with risk and tenure values
    this.http.post(`http://localhost:5000/invest-now/${this.customerId}`, requestData).subscribe(
      (response: any) => {
        this.isLoading = false; // Reset loading state when response is received
        if (response ) {
          console.log('API Response:', response);
          this.creditCardRecommendation = response;
        } else {
          console.error('Error fetching recommendations:', response?.message || 'Undefined response');
        }
      },
      error => {
        this.isLoading = false; // Reset loading state on error
        console.error('API request failed:', error);
        alert('Failed to fetch investment recommendations. Please try again later.');
      }
    );
  }
}
