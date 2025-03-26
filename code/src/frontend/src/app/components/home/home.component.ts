import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { BaseChartDirective } from 'ng2-charts';
import { TransactionService, TransactionData } from '../../services/transaction.service';
import { Chart, ChartConfiguration, ChartType } from 'chart.js';
import { NavbarComponent } from '../navbar/navbar.component';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [
    CommonModule, 
    HttpClientModule,
    BaseChartDirective,
    NavbarComponent
  ],
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {
  userId: string | null = null;
  transactionData: TransactionData | null = null;
  isLoading = true;
  error: string | null = null;

  // Pie Chart Configuration
  public categoryPieChartOptions: ChartConfiguration['options'] = {
    responsive: true,
    plugins: {
      legend: {
        display: true,
        position: 'top',
      }
    }
  };
  public categoryPieChartData: ChartConfiguration['data'] = {
    labels: [],
    datasets: [{ 
      data: [],
      backgroundColor: [
        'rgba(255, 99, 132, 0.7)',
        'rgba(54, 162, 235, 0.7)',
        'rgba(255, 206, 86, 0.7)',
        'rgba(75, 192, 192, 0.7)',
        'rgba(153, 102, 255, 0.7)'
      ]
    }]
  };
  public categoryPieChartType: ChartType = 'pie';

  // Line Chart Configuration
  public loanPaymentsLineChartOptions: ChartConfiguration['options'] = {
    responsive: true,
    scales: {
      y: {
        beginAtZero: true
      }
    }
  };
  public loanPaymentsLineChartData: ChartConfiguration['data'] = {
    labels: [],
    datasets: [{ 
      data: [],
      label: 'Loan Payments',
      borderColor: 'rgba(54, 162, 235, 1)',
      backgroundColor: 'rgba(54, 162, 235, 0.2)',
      fill: true
    }]
  };
  public loanPaymentsLineChartType: ChartType = 'line';

  constructor(private transactionService: TransactionService) {}

  ngOnInit() {
    // Debugging: Log the localStorage access
    console.log('Attempting to retrieve customerId from localStorage');
    this.userId = localStorage.getItem('customerId');
    console.log('Retrieved Customer ID:', this.userId);

    if (this.userId) {
      this.fetchTransactionData();
    } else {
      this.error = 'No customer ID found';
      this.isLoading = false;
      console.error('No customer ID found in localStorage');
    }
  }

  fetchTransactionData() {
    this.isLoading = true;
    this.transactionService.getCustomerTransactions(this.userId!).subscribe({
      next: (data: TransactionData) => {
        console.log('Received transaction data:', data);
        this.transactionData = data;
        this.prepareCategoryPieChart();
        this.prepareLoanPaymentsLineChart();
        this.isLoading = false;
      },
      error: (error) => {
        console.error('Error fetching transaction data', error);
        this.error = error.message;
        this.isLoading = false;
      }
    });
  }

  prepareCategoryPieChart() {
    if (this.transactionData?.category_spending) {
      console.log('Preparing Pie Chart with:', this.transactionData.category_spending);
      this.categoryPieChartData = {
        labels: Object.keys(this.transactionData.category_spending),
        datasets: [{
          data: Object.values(this.transactionData.category_spending),
          backgroundColor: [
            'rgba(255, 99, 132, 0.7)',
            'rgba(54, 162, 235, 0.7)',
            'rgba(255, 206, 86, 0.7)',
            'rgba(75, 192, 192, 0.7)',
            'rgba(153, 102, 255, 0.7)'
          ]
        }]
      };
    } else {
      console.warn('No category spending data available');
    }
  }

  prepareLoanPaymentsLineChart() {
    if (this.transactionData?.loan_payments) {
      console.log('Preparing Line Chart with:', this.transactionData.loan_payments);
      this.loanPaymentsLineChartData = {
        labels: Object.keys(this.transactionData.loan_payments),
        datasets: [{
          data: Object.values(this.transactionData.loan_payments),
          label: 'Loan Payments',
          borderColor: 'rgba(54, 162, 235, 1)',
          backgroundColor: 'rgba(54, 162, 235, 0.2)',
          fill: true
        }]
      };
    } else {
      console.warn('No loan payments data available');
    }
  }

  
}