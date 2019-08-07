%Data sample
mu = 10;
sigma = 4;
DataSize = [ 5, 10, 20, 40, 60, 80, 100, 500, 1000, 10000];

%prior for the mean
mu1 = 10.5;
sigma1 = 1;

figure;
hold;
xlim([1 10000])

for i=1:10
    
N=DataSize(i);    
Data = ((randn(DataSize(i),100)*sigma)+mu);
%ML estimate
muML = mean(Data);

%MAP estimates
MAP1 = (mu1*(sigma^2/N) + muML*sigma1^2)/((sigma^2/N)+sigma1^2);
MAP2 = muML;
for index=1:100
    if muML(index) < 9.5
			MAP2(index) = 9.5;
		elseif muML(index) > 11.5
			MAP2(index) = 11.5;
    end
end
    
err1(i,:) = (abs(muML-mu))/mu;
err2(i,:) = (abs(MAP1-mu))/mu;
err3(i,:) = (abs(MAP2-mu))/mu;

end


subplot(3,1,1);
boxplot(err1');
title('Boxplot for Maximum Likelihood estimate');
set(gca (), "xtick", [1 2 3 4 5 6 7 8 9 10], "xticklabel", {"5", "10", "20", "40", "60", "80", "100","500", "1000", "10000"})

subplot(3,1,2);
boxplot(err2');
title('Boxplot for MAP-1(gaussian prior) estimate');
set(gca (), "xtick", [1 2 3 4 5 6 7 8 9 10], "xticklabel", {"5", "10", "20", "40", "60", "80", "100","500", "1000", "10000"})

subplot(3,1,3);
boxplot(err3');
title('Boxplot for MAP-2(uniform prior) estimate');
set(gca (), "xtick", [1 2 3 4 5 6 7 8 9 10], "xticklabel", {"5", "10", "20", "40", "60", "80", "100","500", "1000", "10000"})

