import { Component,OnInit } from '@angular/core';
import { RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
@Component({
  selector: 'app-navbar',
  imports: [CommonModule, RouterModule], 
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.scss']
})
export class NavbarComponent implements OnInit {
  customerId: string | null = '';
  isDropdownOpen: boolean = false; // Track dropdown state

  constructor(private router: Router) {}

  ngOnInit() {
    // Get customer ID from session storage
    this.customerId = localStorage.getItem('customerId');
  }

  toggleDropdown() {
    this.isDropdownOpen = !this.isDropdownOpen;
  }

  viewProfile() {
    this.router.navigate(['/profile']);
  }

  logout() {
    localStorage.removeItem('customerId');
    this.router.navigate(['/login']);
    this.isDropdownOpen = false;
  }
  
}
