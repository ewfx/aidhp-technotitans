import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
@Component({
  selector: 'app-navbar',
  imports: [CommonModule, RouterModule], 
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.scss']
})
export class NavbarComponent {
  creditCardRecommendation: string | null = null;

  constructor(private http: HttpClient) {}

  fetchCreditCardSuggestions() {
    const customerId = 'CUST001'; // Replace with actual customer ID

    this.http
      .get(`http://localhost:5000/recommend-credit-card/${customerId}`, { responseType: 'text' })
      .subscribe(
        (response) => (this.creditCardRecommendation = response),
        (error) => console.error('Error fetching recommendations:', error)
      );
  }
}
