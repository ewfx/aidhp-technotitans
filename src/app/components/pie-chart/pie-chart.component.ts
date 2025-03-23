import { Component, Input, OnChanges } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ChartConfiguration, ChartType } from 'chart.js';
import { BaseChartDirective } from 'ng2-charts';

@Component({
  selector: 'app-pie-chart',
  imports: [CommonModule, BaseChartDirective], // ✅ No need for NgModule
  templateUrl: './pie-chart.component.html',
})
export class PieChartComponent implements OnChanges {
  @Input() pieChartData!: ChartConfiguration['data'];
  @Input() pieChartOptions: ChartConfiguration['options'] = { responsive: true };

  pieChartType: ChartType = 'pie';

  ngOnChanges() {
    if (this.pieChartData?.datasets?.[0]?.data) {
      const dataLength = this.pieChartData.datasets[0].data.length;
      this.pieChartData.datasets[0].backgroundColor = this.generateColors(dataLength);
    }
  }

  generateColors(count: number): string[] {
    return Array.from({ length: count }, () => 
      `#${Math.floor(Math.random() * 16777215).toString(16).padStart(6, '0')}`
    );
  }
}
