import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';

import { FormsModule } from '@angular/forms';  // Import FormsModule
@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterModule, 
    FormsModule], 
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent { }
