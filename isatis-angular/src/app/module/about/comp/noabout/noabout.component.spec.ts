import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { NoaboutComponent } from './noabout.component';

describe('NoaboutComponent', () => {
  let component: NoaboutComponent;
  let fixture: ComponentFixture<NoaboutComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ NoaboutComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(NoaboutComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
