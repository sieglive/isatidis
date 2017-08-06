import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'isatis-noabout',
  templateUrl: './noabout.component.html',
  styleUrls: ['./noabout.component.scss']
})
export class NoaboutComponent implements OnInit {

  constructor(private router: Router) { }

  ngOnInit() {
  }

}
