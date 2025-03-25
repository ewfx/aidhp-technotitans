import { Component, Input, OnChanges } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ChartConfiguration, ChartType } from 'chart.js';
import { BaseChartDirective } from 'ng2-charts';

@Component({
  selector: 'app-horizontal-bar-chart',
  standalone:true,
  imports: [CommonModule, BaseChartDirective],
  templateUrl: './horizontal-bar-chart.component.html',
})
export class HorizontalBarChartComponent implements OnChanges {
  @Input() barChartData!: ChartConfiguration['data'];
  @Input() barChartOptions: ChartConfiguration['options'] = { responsive: true };

  barChartType: ChartType = 'bar';

  ngOnChanges() {
    if (this.barChartData?.datasets) {
      this.barChartData.datasets.forEach((dataset) => {
        dataset.backgroundColor = this.generateColors(dataset.data.length);
        console.log('Chart Type:', this.barChartType);
        console.log('Chart Options:', this.barChartOptions);
      });
    }

    // Force bars to be horizontal
    if (this.barChartOptions) {
      this.barChartOptions.indexAxis = 'y';
    }
  }

  generateColors(count: number): string[] {
    return Array.from({ length: count }, () => 
      `#${Math.floor(Math.random() * 16777215).toString(16).padStart(6, '0')}`
    );
  }
}
